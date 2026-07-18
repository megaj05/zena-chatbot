/**
 * services/api.js
 * -----------------
 * Thin axios wrapper around the three backend endpoints. Keeping all
 * network calls in one place means components never construct URLs or
 * touch axios directly.
 */

import axios from "axios";
const BASE_URL =
  import.meta.env.VITE_API_URL ||
  "https://Mega05102020.pythonanywhere.com/api";


const client = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

/**
 * Drive the conversation state machine.
 * @param {string} node    current node id (e.g. "main_menu")
 * @param {"menu"|"text"} type how the value was produced
 * @param {string} value   quick-reply id OR free-text message
 */
export async function sendChatMessage(node, type, value) {
  const { data } = await client.post("/chat", { node, type, value });
  return data;
}

/**
 * Submit a lead / collaboration / session form.
 * @param {object} payload  { formType, name, email, phone, requirement,
 *                             category, companyName, purpose }
 */
export async function submitLead(payload) {
  const { data } = await client.post("/lead", payload);
  return data;
}

/** Fetch recent chat history (admin/debug use). */
export async function fetchHistory(limit = 50) {
  const { data } = await client.get(`/history?limit=${limit}`);
  return data;
}

export default { sendChatMessage, submitLead, fetchHistory };
