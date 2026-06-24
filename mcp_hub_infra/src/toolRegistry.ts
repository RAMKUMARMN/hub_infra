// src/tools/toolRegistry.ts

import { discoverCiCdHandler } from "./tools/discoverCiCd.js";
import { discoverEnvironmentVariablesHandler } from "./tools/discoverEnvironmentVariables.js";
import { discoverInfraArchitectureHandler } from "./tools/discoverInfraArchitecture.js";
import { discoverInfrastructureResourcesHandler } from "./tools/discoverInfrastructureResources.js";
import { discoverMessagingConfigHandler } from "./tools/discoverMessagingConfig.js";
import { discoverTerraformModulesHandler } from "./tools/discoverTerraformModules.js";
import { findResourceHandler } from "./tools/findResource.js";

export const toolRegistry = [
  discoverCiCdHandler,
  discoverEnvironmentVariablesHandler,
  discoverInfraArchitectureHandler,
  discoverInfrastructureResourcesHandler,
  discoverMessagingConfigHandler,
  discoverTerraformModulesHandler,
  findResourceHandler,
];