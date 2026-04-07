import express, { type Express, static as serveStatic } from "express";
import cors from "cors";
import pinoHttp from "pino-http";
import path from "path";
import { fileURLToPath } from "url";
import router from "./routes";
import { logger } from "./lib/logger";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app: Express = express();

app.use(
  pinoHttp({
    logger,
    serializers: {
      req(req) {
        return {
          id: req.id,
          method: req.method,
          url: req.url?.split("?")[0],
        };
      },
      res(res) {
        return {
          statusCode: res.statusCode,
        };
      },
    },
  }),
);
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the UI build (for production)
const uiDistPath = path.resolve(__dirname, "../../inventario-ui/dist/public");
app.use(serveStatic(uiDistPath));

app.use("/api", router);

// Fallback middleware for client-side routing - serve index.html for any non-API request
app.use((req, res) => {
  // Skip if it's an API request or if the path has a file extension (static files handled by express.static)
  if (req.path.startsWith("/api") || /\.\w+$/.test(req.path)) {
    return res.status(404).json({ error: "Not found" });
  }
  
  const indexPath = path.join(uiDistPath, "index.html");
  res.sendFile(indexPath, (err) => {
    if (err) {
      logger.error({ err }, "Error sending index.html");
      res.status(404).json({ error: "Not found" });
    }
  });
});

export default app;
