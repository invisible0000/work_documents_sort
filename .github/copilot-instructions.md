# copilot-instructions.md

이 파일은 GitHub Copilot 및 Copilot Chat/Agent와 함께 사용할 때 프로젝트별로 지켜야 할 가이드, 제한, 프롬프트 스타일, 금지사항, 팀 규칙 등을 명시하는 용도로 사용됩니다.

## 목적
- Copilot이 자동화, 코드 생성, 리팩터링, 문서화 등에서 프로젝트의 규칙을 준수하도록 안내합니다.
- 팀/조직의 개발 문화, 코드 스타일, 보안 정책, 금지 패턴, 파일/폴더 무시 규칙 등을 명확히 전달합니다.
- Copilot Agent(자동화 모드) 사용 시, 대규모 변경이나 반복 작업의 기준을 명확히 합니다.

## 예시
- "이 프로젝트의 모든 Python 코드는 PEP8을 준수해야 합니다."
- "테스트 코드는 반드시 test_ 접두어를 사용하세요."
- "개인정보(이메일, 전화번호 등)는 코드/주석/문서에 포함하지 마세요."
- "자동화 작업은 반드시 dry-run 옵션을 먼저 사용하세요."
- "특정 폴더(src/legacy)는 Copilot 자동 리팩터링에서 제외하세요."

## 작성 가이드
- 마크다운 형식으로 작성합니다.
- 명확하고 구체적으로 작성합니다.
- 팀/조직의 정책, 코드 스타일, 워크플로, 금지사항, 예외사항 등을 포함할 수 있습니다.
- 예시, 금지/권장 패턴, 참고 링크 등을 자유롭게 추가하세요.

## 참고
- [Copilot 공식 문서](https://docs.github.com/en/copilot)
- [Copilot Chat/Agent 모드 안내](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)

---

> 이 파일을 .github 폴더에 두면 Copilot이 더 일관성 있게 팀의 규칙을 따릅니다.
