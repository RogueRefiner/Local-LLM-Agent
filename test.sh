curl -X POST "http://0.0.0.0:8000/prompt" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
        --rawfile prompt prompt.txt \
        '{prompt: $prompt, template_name: "generate_docstring"}')"