export async function discoverInfraArchitectureHandler() {
  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(
          {
            infrastructure: "Terraform",
            messaging: "Mosquitto MQTT",
            ciCd: "GitHub Actions",
            structure: [
              "terraform/",
              "terraform/modules/",
              "mosquitto/",
              "workflows/"
            ]
          },
          null,
          2
        ),
      },
    ],
  };
}