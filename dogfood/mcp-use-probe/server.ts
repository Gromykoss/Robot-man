import { MCPServer } from "mcp-use";
import { z } from "zod";
import { readFileSync } from "fs";

const server = new MCPServer({
  name: "robotman-ops",
  version: "0.1.0",
});

export const recentPosts = server.tool(
  {
    name: "recent_posts",
    description: "Last N posts published by @RobotsTJ500 from published_posts.jsonl",
    inputSchema: z.object({
      count: z.number().int().min(1).max(20).default(5),
    }),
    outputSchema: z.object({
      posts: z.array(z.object({ id: z.string(), text: z.string(), ts: z.string() })),
    }),
  },
  async ({ count }) => {
    const lines = readFileSync("/home/hermes-workspace/robot-man/published_posts.jsonl", "utf8")
      .trim().split("\n").slice(-count);
    const posts = lines.map((l) => {
      const j = JSON.parse(l);
      const text = j.text || j.tweet_text || j.content || "";
      return { id: String(j.id || j.tweet_id || ""), text: String(text).slice(0, 140), ts: String(j.created_at || j.timestamp || "") };
    });
    const pdata = { posts };
    return { content: [{ type: "text", text: JSON.stringify(pdata) }], structuredContent: pdata };
  },
);

export const graphStats = server.tool(
  {
    name: "graph_stats",
    description: "Entity/edge counts of the robot-man Knowledge Graph",
    inputSchema: z.object({}),
    outputSchema: z.object({ entities: z.number(), edges: z.number() }),
  },
  async () => {
    const g = JSON.parse(readFileSync("/home/hermes-workspace/robot-man/knowledge_graph/graph.json", "utf8"));
    const e = g.entities || g.nodes || {};
    const ed = g.edges || g.relations || [];
    const data = { entities: Array.isArray(e) ? e.length : Object.keys(e).length, edges: Array.isArray(ed) ? ed.length : Object.keys(ed).length };
    return { content: [{ type: "text", text: JSON.stringify(data) }], structuredContent: data };
  },
);

server.listen(3000).then(() => console.log("listening 3000"));
export default server;
