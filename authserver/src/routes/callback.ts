import { Request, Response, NextFunction } from "express";
import { Code } from "../models/auth";
import { BOT_USERNAME } from "../util/secrets";
import logger from "../util/logging";

export const callbackRoute = async (req: Request, res: Response, next: NextFunction) => {
    try {
        if (req.query.error) return res.send("Cancelled");
        const userIp = req.connection.remoteAddress;
        let code = await Code.findOneAndUpdate(
            { ip: userIp },
            {
                authCode: req.query.code,
            },
            { new: true }
        );

        if (!code) {
            code = new Code({
                authCode: req.query.code,
                ip: userIp,
            });
            await code.save();
            res.redirect(`https://t.me/${BOT_USERNAME}?start=${code._id}`);
        } else {
            res.redirect(`https://t.me/${BOT_USERNAME}?start=${code._id}`);
        }
    } catch (err: any) {
        logger.log({
            level: "info",
            message: err.message,
        });
        res.status(500).json({ error: "Internal server error" });
    }
};

export const homeRoute = async (req: Request, res: Response, next: NextFunction) => {
    res.status(200).send("Welcome to spotipie authserver");
};
