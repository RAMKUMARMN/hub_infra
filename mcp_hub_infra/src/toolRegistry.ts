// src/tools/toolRegistry.ts

import { discoverCiCd } from "./discoverCiCd";
import { discoverEnvironmentVariables } from "./discoverEnvironmentVariables";
import { discoverInfraArchitecture } from "./discoverInfraArchitecture";
import { discoverInfrastructureResources } from "./discoverInfrastructureResources";
import { discoverMessagingConfig } from "./discoverMessagingConfig";
import { discoverTerraformModules } from "./discoverTerraformModules";
import { findResource } from "./findResource";

export const toolRegistry = [
  discoverCiCd,
  discoverEnvironmentVariables,
  discoverInfraArchitecture,
  discoverInfrastructureResources,
  discoverMessagingConfig,
  discoverTerraformModules,
  findResource,
];