import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { discoverInfraArchitectureHandler } from "./tools/discoverInfraArchitecture.js";
import { discoverTerraformModulesHandler } from "./tools/discoverTerraformModules.js";
import { discoverInfrastructureResourcesHandler } from "./tools/discoverInfrastructureResources.js";
import { discoverCiCdHandler } from "./tools/discoverCiCd.js";
import { discoverMessagingConfigHandler } from "./tools/discoverMessagingConfig.js";
import { discoverEnvironmentVariablesHandler } from "./tools/discoverEnvironmentVariables.js";
import { findResourceHandler } from "./tools/findResource.js";

const server = new McpServer({
  name: "hub-infra-mcp",
  version: "1.0.0",
});

server.tool(
  "discover_infra_architecture",
  "Discover infrastructure architecture and repository structure",
  {},
  discoverInfraArchitectureHandler
);

server.tool(
  "discover_terraform_modules",
  "Discover Terraform modules",
  {},
  discoverTerraformModulesHandler
);

server.tool(
  "discover_infrastructure_resources",
  "Discover infrastructure resources",
  {},
  discoverInfrastructureResourcesHandler
);

server.tool(
  "discover_ci_cd",
  "Discover CI/CD workflows",
  {},
  discoverCiCdHandler
);

server.tool(
  "discover_messaging_config",
  "Discover messaging and MQTT configuration",
  {},
  discoverMessagingConfigHandler
);

server.tool(
  "discover_environment_variables",
  "Discover Terraform environment variables",
  {},
  discoverEnvironmentVariablesHandler
);

server.tool(
  "find_resource",
  "Find infrastructure resources and related files",
  {
    resource: z.string(),
  },
  findResourceHandler
);

async function main() {
  const transport = new StdioServerTransport();

  await server.connect(transport);

  console.error("Hub Infra MCP Server Running...");
}

main().catch(console.error);