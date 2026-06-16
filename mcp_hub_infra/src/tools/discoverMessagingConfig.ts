import fs from "fs";
import path from "path";
import { HUB_INFRA_PATH } from "../config.js";

export async function discoverMessagingConfigHandler() {
  const configPath = path.join(
    HUB_INFRA_PATH,
    "mosquitto",
    "mosquitto.conf"
  );

  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(
          {
            broker: "Mosquitto MQTT",
            configExists: fs.existsSync(configPath),
            configPath: "mosquitto/mosquitto.conf"
          },
          null,
          2
        ),
      },
    ],
  };
}