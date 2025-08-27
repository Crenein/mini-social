---
applyTo: '**'
---
# GitHub Copilot Chat Instructions

## Code Generation Rules

- **No automatic README files**: Do not create README or explanatory documentation files unless explicitly requested by the user.

- **No automatic testing**: Do not generate unit tests, simulations, or test files unless the user specifically asks for them.

- **Ask before creating files**: Never create new files automatically. Always ask the user for permission before creating any new file.

- **Explain before implementing**: When the user says "explain before implementing", provide a simple explanation of the implementation plan and ask if they want to proceed with the suggested implementation.

- **Simple comments only**: Add only simple, concise comments to code. Avoid verbose or overly detailed explanations in comments.

## Response Format

- Keep explanations brief and to the point
- Ask for confirmation before taking actions that create new files
- Focus on code modifications rather than file creation
- Prioritize user control over automatic actions