import dotenv from "dotenv";
import fs from "fs";

if (fs.existsSync(".env")) {
    console.log("Using .env file to supply config environment variables");
    dotenv.config({ path: ".env" });
}

// TODO: MONGO_HOST (related to NODE_ENV)
export const MONGO_USER = process.env["MONGO_USER"];
export const MONGO_PASSWORD = process.env["MONGO_PASSWORD"];
export const MONGO_DB = process.env["MONGO_DB"] || "spotipie";
// FIXME: Take environment into consideration

if (!MONGO_USER) {
    console.log("No mongo user. Set MONGO_USER environment variable.");
}

if (!MONGO_PASSWORD) {
    console.log("No mongo password. Set MONGO_PASSWORD environment variable.");
}

export const MONGODB_URI = `mongodb://${MONGO_USER}:${MONGO_PASSWORD}@mongo:27017/${MONGO_DB}`;
export const BOT_USERNAME = process.env["BOT_USERNAME"];

if (!BOT_USERNAME) {
    console.log("No bot username. Set BOT_USERNAME environment variable.");
}
