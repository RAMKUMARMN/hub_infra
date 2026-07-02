export async function discoverInfrastructureResourcesHandler() {
  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(
          {
            resources: [
              "VPC",
              "RDS",
              "S3",
              "ElastiCache",
              "Mosquitto"
            ]
          },
          null,
          2
        ),
      },
    ],
  };
}