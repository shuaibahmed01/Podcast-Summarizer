const express = require('express');
const multer = require('multer');
const { Configuration, OpenAIApi } = require('openai');
const fs = require('fs');
const cors = require('cors');
require('dotenv').config();

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(cors());
app.use(express.json());

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

app.post('/process-audio', upload.single('audio'), async (req, res) => {
  try {
    const audioFile = req.file;
    const email = req.body.email;

    // 1. Transcribe the audio file
    const transcript = await openai.createTranscription(
      fs.createReadStream(audioFile.path),
      "whisper-1"
    );

    // 2. Generate a summary using GPT-3.5 or GPT-4
    const completion = await openai.createChatCompletion({
      model: "gpt-4o",
      messages: [
        { role: "system", content: "You are a helpful assistant that creates a structured report of the podcast. A user should completely understand what the podcast was about and any important information from the report you geenrate" },
        { role: "user", content: `Please provide a comprehensive summary of the following podcast transcript, including the main topic, main points, and key takeaways:\n\n${transcript.data.text}` }
      ],
    });

    const summary = completion.data.choices[0].message.content;

    // 3. Parse the summary into structured data
    const structuredSummary = {
      title: "Podcast Summary", // You might want to extract this from the summary
      summary: summary, // Extract interesting facts or cool points from the summary
    };

    // 4. Send the summary back to the client
    res.json({ summary: structuredSummary });

    // 5. Clean up the uploaded file
    fs.unlinkSync(audioFile.path);

  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'An error occurred while processing the audio file.' });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});