// Simple TypeScript agent for handling requests

interface Request {
    task: string;
    data?: any;
}

interface Response {
    result: string;
    success: boolean;
}

class Agent {
    async handleRequest(req: Request): Promise<Response> {
        console.log(`Processing task: ${req.task}`);
        // Simulate processing
        await new Promise(resolve => setTimeout(resolve, 100));
        return {
            result: `Processed ${req.task}`,
            success: true
        };
    }
}

export default Agent;