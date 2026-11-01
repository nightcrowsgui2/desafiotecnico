"""Terminal chat with the agent: python -m agent [--debug]"""

import json
import sys
from datetime import datetime

from dotenv import load_dotenv

from agent.store import ROOT

TRANSCRIPTS_DIR = ROOT / "transcripts"


def format_call(call: dict) -> str:
    args = ", ".join(f"{k}={v!r}" for k, v in call["args"].items())
    return f"{call['tool']}({args})"


def main() -> None:
    load_dotenv(ROOT / ".env")
    from agent.chat import StoreAgent  # after load_dotenv, so the client sees GEMINI_API_KEY

    debug = "--debug" in sys.argv
    agent = StoreAgent()
    started = datetime.now()
    lines = [f"# Conversa — {started:%d/%m/%Y %H:%M}", "", f"Modelo: `{agent.model}`", ""]

    print("Empório da Música — atendimento virtual. Digite 'sair' para encerrar.\n")
    while True:
        try:
            message = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if message.lower() in {"sair", "exit", "quit"}:
            break
        if not message:
            continue

        try:
            reply, calls = agent.send(message)
        except Exception as e:  # network/quota errors should not kill the conversation
            print(f"[erro ao falar com o modelo: {e}]\n")
            continue

        for call in calls:
            if debug:
                print(f"  ↳ {format_call(call)}")
        print(f"\nLia: {reply}\n")

        lines += [f"**Cliente:** {message}", ""]
        if calls:
            lines.append("<details><summary>Ferramentas consultadas</summary>\n")
            for call in calls:
                result = call["result"]
                if isinstance(result, str):
                    lines += [f"`{format_call(call)}`", "", "```text", result, "```", ""]
                else:
                    result = json.dumps(result, ensure_ascii=False, indent=2)
                    lines += [f"`{format_call(call)}`", "", "```json", result, "```", ""]
            lines += ["</details>", ""]
        lines += [f"**Lia:** {reply}", ""]

    if len(lines) > 4:
        TRANSCRIPTS_DIR.mkdir(exist_ok=True)
        path = TRANSCRIPTS_DIR / f"{started:%Y%m%d-%H%M%S}.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Conversa salva em {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
