import os, re, json, time
import openai
from colorama import Fore, Style
import sglang as sgl

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GMAIL_APP_KEY = os.getenv('GMAIL_APP_KEY')
EMAIL = os.getenv('EMAIL')

client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
)

stop = ['Observation:', 'Observation ']
MAX_ITERATION = 10

EMAIL_DB=f"""
NAME		EMAIL
Steve Jobs: sjobs@apple.com
Test:  test@gmail.com
Liu: {EMAIL}
"""

@sgl.function
def find_email(s, query: str):
    s += sgl.user("The following lists names and email addresses of my contacts:\n"+EMAIL_DB+"\n Please return email of "+query)
    s += sgl.assistant(sgl.gen("query_result"))

def send_email_internal(to_addr: str, subject: str, body: str) -> str:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # SMTP server configuration
    smtp_server = "smtp.gmail.com"  # This might need to be updated
    smtp_port = 587  # or 465 for SSL
    username = EMAIL
    password = GMAIL_APP_KEY
    from_addr = EMAIL

    cc_addr = ""

    # Email content

    # Setting up the MIME
    message = MIMEMultipart()
    message["From"] = from_addr
    message["To"] = to_addr
    message["Subject"] = subject
    # message["Cc"] = cc_addr  # Add CC here
    message.attach(MIMEText(body, "plain"))

    recipients = [to_addr, cc_addr]  # List of all recipients

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(username, password)
            text = message.as_string()
            server.sendmail(from_addr, recipients, text)
            output = "Email successfully sent!"
    except Exception as e:
        output = f"Failed to send email: {e}"
    print(output)
    return output

def send_email(llm_json_str: str) -> str:
    try:
        patch_json_content = json.loads(llm_json_str)
        to_addr = patch_json_content["to_addr"]
        subject = patch_json_content["subject"]
        body = patch_json_content["body"]

    except Exception as e:
        error_str = f"Exception: {e}"

    print(f"To: {to_addr}\n{subject}\n==============================\n{body}\n=================================\n")
    approval = input("Is the above email good to go? (yes/no): ")
    if approval.lower() == 'yes' or approval.lower() == 'y':
        # TODO: send email
        output = send_email_internal(to_addr, subject, body)
        # output = "email sent successfully"
    else:
        output = f"Email sending was not approved. Reason for disapproval: {approval}"

    return output

from string import Template
tao_template=Template("""
My name is Hanzhong Liu. You are my email assistant, Monica. You have access to the following tools:
                 
    FindEmail: "Find the email addresses of my contacts. Input is the contact info such as names."
    SendEmail: "Send email tool. Input is a json object with {"to_addr: str, "subject": str, "body": str"}."

To craft an email, you should use FindEmail to find correct email addresses (to_addr) of my contacts.

Use the following format:
    
    Thought: you should always think about what to do
    Action: the action to take, should be one of [FindEmail, SendEmail]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I have now completed the task 
    Done: the final message to the task
    
Always generate Action and Action Input. Missing them will produce an error!
    
    Begin!               
    
    Question:
    $question

    Thought:
""")



@sgl.function
def llm_do_task_sglang(s, question: str):
    prompt = str(tao_template.substitute(question=question))
    s += sgl.user(prompt)

    iteration = 0
    while True:
        print(Fore.YELLOW + f"\n\n========================== Iteration: {iteration} ========================= ")

        iteration = iteration + 1
        if iteration > MAX_ITERATION:
            break

        # Invoke SGLang
        s += sgl.assistant(
            sgl.gen(
                name=f"iteration-{iteration}",
                stop=stop
            )
        )
        llm_output = s[f"iteration-{iteration}"]

        # format verify
        # Action: ....
        # Action Input: ......
        regex = (
            r"Action\s*\d*\s*:[\s]*(.*?)[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        )
        action_match = re.search(regex, llm_output, re.DOTALL)

        if action_match:

            action = action_match.group(1).strip()
            action_input = action_match.group(2)
            tool_input = action_input.strip("\n")

            print(Fore.GREEN + f"> Invoke Tool: {action}")
            print(Fore.GREEN + f"> Input: {tool_input}\n")
            print(Style.RESET_ALL)

            # if llm_output.startswith("Thought:"):
            #     # prompt = prompt + llm_output[8:]
            #     # s += response[]
            #     s += sgl.user(llm_output)
            # else:
            #     s += sgl.user(llm_output)

            if action == "SendEmail":
                tool_output = send_email(tool_input)
                if "Email successfully sent!" in tool_output:
                    return

            elif action == "FindEmail":
                r = find_email.run(query=tool_input)
                tool_output = r['query_result']

            else:
                tool_output = "Error: Action " + f"'{action}' is not a valid!"

            print(f"------- tool_output ------- \n{tool_output}\n")

        elif 'Done:' in llm_output:
            print(f"\n\n{llm_output}")
            return

        else:
            print(f"Error: wrong LLM response\n{llm_output}\n")

        s += sgl.user("\nObservation: " + str(tool_output) + "\n")
        # prompt = prompt + "\nObservation: " + str(tool_output) + "\n"


sgl.set_default_backend(sgl.OpenAI("chatgpt-4o-latest"))
print(f"I'm your email assistant, Monica.")
while True:
    try:
        user_input = input("Please enter a new task: ")
        tic = time.time()
        # llm_do_task(user_input)

        llm_do_task_sglang.run(
            user_input
        )

        latency = time.time() - tic
        print(f"\nLatency: {latency:.3f}s")
    except KeyboardInterrupt:
            print("\nExiting.\n")
            break