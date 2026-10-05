import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const client = new Client({ name: "probe-http", version: "0.1.0" });
await client.connect(new StreamableHTTPClientTransport(new URL("http://localhost:3000/mcp")));
const tools = await client.listTools();
console.log("TOOLS:", tools.tools.map((t) => t.name).join(", "));
const posts = await client.callTool({ name: "recent_posts", arguments: { count: 3 } });
console.log("recent_posts OK, n =", JSON.parse(JSON.stringify(posts)).content?.[0]?.text?.length ?? "?");
const gs = await client.callTool({ name: "graph_stats", arguments: {} });
console.log("graph_stats:", gs.content?.[0]?.text?.slice(0, 200));
await client.close();
process.exit(0);
