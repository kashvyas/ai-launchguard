"""Start AI LaunchGuard v0.2 conversational analyst: python -m src.ai_launchguard.chat_cli"""
from .assistant import QuestionError,ReleaseAssistant

def main():
    app=ReleaseAssistant()
    print("AI LaunchGuard v0.2 • /quit to exit")
    while True:
        try: question=input("\nAsk: ").strip()
        except (EOFError,KeyboardInterrupt): break
        if question.lower() in {"/quit","/exit"}: break
        try: result=app.ask(question)
        except QuestionError as exc:
            print("Input:",exc)
            continue
        print("DECISION:",result["decision"],"| APPROVED:",str(result["approved_rollout_pct"])+"%")
        print("REASONS:","; ".join(result["reasons"]))
        print("LLM ANALYSIS (advisory):",result["analysis"])
if __name__=="__main__":main()
