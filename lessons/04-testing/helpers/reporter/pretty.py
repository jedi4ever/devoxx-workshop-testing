from inspect_ai.log import read_eval_log, EvalLog, EvalLogInfo, list_eval_logs
from inspect_ai.dataset import Sample

from colorama import Fore, Back, Style

def pretty_message(message):
    output = []
    #print(message)
    # pad message.role to 10 chars
    message_role = message.role
    model=""
    if(message_role == "assistant"):
       model=message.model

       if (message.tool_calls):
            for tool_call in message.tool_calls:
               output.append(f"{Fore.YELLOW} {message_role.ljust(10)}[tool:{tool_call.function}] {Fore.RESET}> {tool_call.arguments}" )
            # tool_calls
            # "function": "security_vulnerability_scanner",
            # "arguments": {
            #"code": "console.log('patrick')"
            #}


    if (message_role == "tool"):
        message_role = f"{message_role}[{message.function}]"
        #print(message)


    message_content = message.content
    # print(message_content.__class__)
    if (isinstance(message_content, str)):
        output.append(f"{Fore.YELLOW} {message_role.ljust(10)} {Fore.RESET}> {message.content}")
    elif (isinstance(message_content,list)):
        for m in message_content:
            match m.type:
                case "text":            
                    output.append(f"{Fore.YELLOW} {message_role.ljust(10)} {Fore.RESET}+> {m.text}")
                case "image":
                    output.append("")
                case "video":
                    output.append("")
                case "reasoning":
                    output.append(f"{Fore.YELLOW} {message_role.ljust(10)} {Fore.RESET}+> {m.reasoning}")
    return output

def pretty_scorer(scorer,value):
    output = []
    #print(value)
    output.append(f"Scorer[{scorer}][VALUE]: {value.value}")
    #print(f"Scorer[{scorer}][ANSWER]: {value.answer}")
    output.append(f"Scorer[{scorer}][EXPLANATION]: {value.explanation}")
    # value.answer
    # value.explanation
    return output


def pretty_sample(sample: Sample,show_events=False):
#    print(sample)
    output = []

    output.append("======= Sample Begin =================================================================")
    output.append(f"input : {sample.input}")
    output.append(f"target: {sample.target}")

    output.append("======================================================================================")
    for message in sample.messages:
        message_output = pretty_message(message)
        output.extend(message_output)

    if (show_events):
        for event in sample.events:
            #print(event)
            output.append(f"event-----> {event.event}:")

            match event.event:
                case "step":
                    output.append(event.action)
                    output.append(event.type)
                    output.append(event.name)
                    output.append(event)
                case "model":
                    output.append(event.model)
                case "state":
                    for change in event.changes:
                        output.append(change)
                case "score":
                    output.append(event.score)
                case "sample_init":
                    output.append(event.sample)
                case _:
                    output.append(event)

    output.append("======== Score =======================================================================")
    for scorer, value in sample.scores.items():
        scorer_output = pretty_scorer(scorer,value)
        output.extend(scorer_output)
    output.append("======================================================================================")

    return output

def pretty_results(results: list[EvalLog],show_events=False):
    output = []
    for r in results:
        if is_notebook():
            from IPython.display import HTML
            from IPython.display import display as IPython_display
            from IPython.display import HTML
            IPython_display(HTML("""<a href="%s">%s</a>"""%(r.location, r.location)))
        else:
            output.append(r.location)
        print(f"Status: {r.status} Model: {r.eval.model}")
        for s in r.samples:
            sample_output = pretty_sample(s,show_events=show_events)
            output.extend(sample_output)

        output.append("**** End Sample ******************************************************************")

    return "\n".join(output)

# https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter
