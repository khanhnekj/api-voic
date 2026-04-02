import TelegramBot from "node-telegram-bot-api";
import fetch from "node-fetch";
import fs from "fs";

// 🔥 token bot telegram của bạn
const TOKEN = "8527306361:AAGmrlHpP6Z-QLiKehY8Zx5L3QuQ4ZGt2Ik";

const bot = new TelegramBot(TOKEN, { polling: true });

// ===============================
// 🚀 lệnh /voice
// ===============================
bot.onText(/\/voice (.+)/, async (msg, match) => {
  const chatId = msg.chat.id;
  const text = match[1];

  if (!text) {
    return bot.sendMessage(chatId, "Thiếu nội dung");
  }

  try {
    bot.sendMessage(chatId, "🔊 đang tạo voice...");

    const res = await fetch("https://voic-z.onrender.com/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text, lang: "vi" })
    });

    const file = fs.createWriteStream("voice.mp3");

    await new Promise((resolve, reject) => {
      res.body.pipe(file);
      res.body.on("error", reject);
      file.on("finish", resolve);
    });

    await bot.sendAudio(chatId, "voice.mp3");

  } catch (err) {
    console.log(err);
    bot.sendMessage(chatId, "❌ lỗi API TTS");
  }
});

// ===============================
// 🚀 lệnh !voice (chat thường)
// ===============================
bot.on("message", async (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;

  if (!text || text.startsWith("/voice")) return;

  if (text.startsWith("!voice ")) {
    const t = text.slice(7);

    bot.sendMessage(chatId, "🔊 đang đọc...");

    const res = await fetch("https://voic-z.onrender.com/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: t, lang: "vi" })
    });

    const file = fs.createWriteStream("voice.mp3");

    await new Promise((resolve, reject) => {
      res.body.pipe(file);
      res.body.on("error", reject);
      file.on("finish", resolve);
    });

    await bot.sendAudio(chatId, "voice.mp3");
  }
});
