const OpenAI = require('openai');

async function main() {
    // Retrieve API key from environment variable
    const apiKey = process.env.NVIDIA_API_KEY || '$API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC';

    // Initialize OpenAI client with NVIDIA's base URL
    const openai = new OpenAI({
        apiKey: apiKey,
        baseURL: 'https://integrate.api.nvidia.com/v1',
    });

    try {
        // Create a chat completion request
        const completion = await openai.chat.completions.create({
            model: "deepseek-ai/deepseek-r1",
            messages: [{"role": "user", "content": "Which number is larger, 9.11 or 9.8?"}],
            temperature: 0.6,
            top_p: 0.7,
            max_tokens: 4096,
            stream: true
        });

        // Stream and print the response
        console.log("DeepSeek AI Response:");
        for await (const chunk of completion) {
            process.stdout.write(chunk.choices[0]?.delta?.content || '');
        }
    } catch (error) {
        console.error('Error interacting with DeepSeek AI:', error);
    }
}

main();
