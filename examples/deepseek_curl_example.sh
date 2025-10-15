#!/bin/bash

# DeepSeek AI Interaction using cURL

# Configuration
invoke_url='https://integrate.api.nvidia.com/v1/chat/completions'
api_key="${NVIDIA_API_KEY:-$API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC}"

# Headers
authorization_header="Authorization: Bearer $api_key"
accept_header='Accept: application/json'
content_type_header='Content-Type: application/json'

# Request payload
data=$(cat <<EOF
{
  "messages": [
    {
      "role": "user",
      "content": "Which number is larger, 9.11 or 9.8?"
    }
  ],
  "stream": true,
  "model": "deepseek-ai/deepseek-r1",
  "max_tokens": 4096,
  "presence_penalty": 0,
  "frequency_penalty": 0,
  "top_p": 0.7,
  "temperature": 0.6
}
EOF
)

# Make the API call
echo "Sending request to DeepSeek AI..."
response=$(curl --silent -i -w "\n%{http_code}" --request POST \
  --url "$invoke_url" \
  --header "$authorization_header" \
  --header "$accept_header" \
  --header "$content_type_header" \
  --data "$data"
)

# Process and display the response
echo "Response:"
echo "$response"
