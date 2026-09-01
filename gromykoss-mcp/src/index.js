import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// MCP-сервер портфолио gromykoss.crab-ailab.com
// Read-only тула: кто такой Сергей, что за агентная ферма, свежие посты, контакт.
// Без аутентификации (этап 2а); OAuth 2.1 добавим на этапе 2б.

export class GromykossMCP extends McpAgent {
	server = new McpServer({
		name: "gromykoss-portfolio",
		version: "1.0.0",
		description: "MCP interface for Sergey Gromyko's portfolio — AI systems engineer, autonomous multi-agent systems in production.",
	});

	async init() {
		// Кто такой Сергей — краткое досье
		this.server.tool(
			"who_is_sergey",
			"Get a short bio of Sergey Gromyko: construction project director (14+ years) who built an autonomous multi-agent system managing his own domain.",
			{},
			async () => ({
				content: [
					{
						type: "text",
						text: [
							"Sergey Gromyko — AI Systems Engineer.",
							"",
							"Construction project director with 14+ years of experience who automated his own domain:",
							"- Hierarchical multi-agent farm: 8 agent profiles, 29+ jobs executed",
							"- Production WhatsApp agent (Alikhan) managing a 2700-hectare construction site",
							"- MoA (Mixture of Agents) verification pipeline for content quality",
							"- 9x cost reduction vs. commercial alternatives",
							"- Code and architecture public",
							"",
							"Portfolio: https://gromykoss.crab-ailab.com",
							"X: https://x.com/gromykoss",
						].join("\n"),
					},
				],
			})
		);

		// Агентная ферма — архитектура
		this.server.tool(
			"agent_farm_architecture",
			"Get the architecture of Sergey's multi-agent farm: profiles, roles, communication channels.",
			{},
			async () => ({
				content: [
					{
						type: "text",
						text: [
							"Multi-Agent Farm Architecture (production since 2026):",
							"",
							"Profiles (8):",
							"- Hermes — chief of staff / infrastructure director",
							"- Alikhan — site agent (WhatsApp bridge, 2700 ha construction)",
							"- Robot-man — X/Twitter content agent (2 accounts)",
							"- GULAG — secure messenger project agent",
							"- RAB9 — crypto signals agent",
							"- Job-hunter — career dossier agent",
							"- Grok-bot — office specialist (drawings, invoices, BOQ)",
							"- +1 niche profile",
							"",
							"Channels: Telegram (direct), WhatsApp (Alikhan bridge), agent-bus (Buzz relay).",
							"Verification: MoA pipeline (multiple models cross-review).",
							"",
							"Details and diagrams: https://gromykoss.crab-ailab.com",
						].join("\n"),
					},
				],
			})
		);

		// Свежие посты @RobotsTJ500 и @gromykoss
		this.server.tool(
			"recent_posts",
			"Get recent public posts from Sergey's X accounts (@gromykoss personal, @RobotsTJ500 agent-run).",
			{ account: z.enum(["gromykoss", "robotstj500", "both"]).default("both").describe("Which account's posts to fetch") },
			async ({ account }) => {
				// RSS-фид nitter-инстанса ненадёжен; используем прямые данные (обновляются вручную/кроном)
				const data = {
					gromykoss: [
						{ date: "2026-08-31", text: "We onboarded a new teammate — Grok-bot from the client's office, running on Grok models. After a few days on drawings, invoices, BOQ and material requests, I wired him into the team.", url: "https://x.com/Gromykoss/status/2094492762087539118" },
					],
					robotstj500: [
						{ date: "2026-08-31", text: "Agent context loop post: how one director agent + 5 profiles keep context across human approval cycles without breaking the thread.", url: "https://x.com/RobotsTJ500/status/2094423680012960043" },
					],
				};
				let payload;
				if (account === "both") {
					payload = [...data.gromykoss, ...data.robotstj500];
				} else {
					payload = data[account];
				}
				return {
					content: [
						{
							type: "text",
							text: payload.map((p) => `${p.date} — ${p.text}\n${p.url}`).join("\n\n"),
						},
					],
				};
			}
		);

		// Контакт / как связаться
		this.server.tool(
			"contact",
			"Get contact channels for Sergey Gromyko.",
			{},
			async () => ({
				content: [
					{
						type: "text",
						text: [
							"Contact Sergey Gromyko:",
							"- X (preferred): https://x.com/gromykoss",
							"- Portfolio: https://gromykoss.crab-ailab.com",
							"- Agent-run account: https://x.com/RobotsTJ500",
							"",
							"Serious inquiries: construction automation, multi-agent systems consulting, production agent deployment.",
						].join("\n"),
					},
				],
			})
		);
	}
}

export default {
	fetch(request, env, ctx) {
		const url = new URL(request.url);
		if (url.pathname === "/mcp") {
			return GromykossMCP.serve("/mcp").fetch(request, env, ctx);
		}
		// CORS/health
		if (url.pathname === "/") {
			return new Response(
				JSON.stringify({
					server: "gromykoss-portfolio-mcp",
					version: "1.0.0",
					endpoint: "/mcp",
					transport: "streamable-http",
				}),
				{ headers: { "content-type": "application/json" } }
			);
		}
		return new Response("Not found", { status: 404 });
	},
};
