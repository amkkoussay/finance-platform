import api from "./api";

export const CATEGORIES = [
  "food",
  "transport",
  "utilities",
  "entertainment",
  "other",
  "salary",
];

/** Create a new transaction. `data` must include user_id, date, category, amount, description, is_income. */
export async function createTransaction(data) {
  try {
    const response = await api.post("/transactions", data);
    return { success: true, transaction: response.data.transaction };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Fetch all transactions for a user, newest first. */
export async function getTransactions(userId) {
  try {
    const response = await api.get("/transactions", { params: { user_id: userId } });
    return { success: true, transactions: response.data.transactions };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Update an existing transaction. `data` must include user_id and the editable fields. */
export async function updateTransaction(id, data) {
  try {
    const response = await api.put(`/transactions/${id}`, data);
    return { success: true, transaction: response.data.transaction };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Delete a transaction owned by userId. */
export async function deleteTransaction(id, userId) {
  try {
    await api.delete(`/transactions/${id}`, { params: { user_id: userId } });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Upload a CSV file of transactions for bulk import. */
export async function bulkUpload(userId, file) {
  try {
    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("file", file);

    const response = await api.post("/transactions/bulk-upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return { success: true, imported: response.data.imported, errors: response.data.errors };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
