import * as fs from "fs";
import path from "path";
import {HUB_INFRA_PATH} from "../config.js";

export async function findResourceHandler({
  resource,
}: {
  resource: string;
}) {
  const root = path.join(
    HUB_INFRA_PATH,
    "app"
  );

  const resources: string[] = [];

  const searchDirectory = (dir: string, depth: number = 0) => {
    if (depth > 5) return;

    try {
      const files = fs.readdirSync(dir);

      for (const file of files) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory() && !file.startsWith(".")) {
          if (file.toLowerCase().includes(resource.toLowerCase())) {
            resources.push(path.relative(HUB_INFRA_PATH, fullPath));
          }
          searchDirectory(fullPath, depth + 1);
        } else if (stat.isFile()) {
          if (file.toLowerCase().includes(resource.toLowerCase())) {
            resources.push(path.relative(HUB_INFRA_PATH, fullPath));
          }
        }
      }
    } catch (error) {
      // Handle cases where directory cannot be read
    }
  };

  searchDirectory(root);

  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(
          {
            resource,
            found: resources.length > 0,
            locations: resources,
          },
          null,
          2
        ),
      },
    ],
  };
}
