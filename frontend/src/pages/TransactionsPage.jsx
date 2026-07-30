import { useCallback, useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";
import {
  createTransaction,
  deleteTransaction,
  getTransactions,
  bulkUpload,
} from "../services/transactions";
import TransactionForm from "../components/TransactionForm";
import TransactionTable from "../components/TransactionTable";
import BulkUpload from "../components/BulkUpload";
import Loading from "../components/Loading";
import ErrorAlert from "../components/ErrorAlert";

export default function TransactionsPage() {
  const { user } = useAuth();
  const [transactions, setTransactions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const loadTransactions = useCallback(async () => {
    setIsLoading(true);
    const result = await getTransactions(user.user_id);
    if (result.success) {
      setTransactions(result.transactions);
      setError("");
    } else {
      setError(result.error);
    }
    setIsLoading(false);
  }, [user.user_id]);

  useEffect(() => {
    loadTransactions();
  }, [loadTransactions]);

  async function handleCreate(formData) {
    setIsSubmitting(true);
    const result = await createTransaction({ ...formData, user_id: user.user_id });
    setIsSubmitting(false);

    if (result.success) {
      await loadTransactions();
    }
    return result;
  }

  async function handleDelete(id) {
    const result = await deleteTransaction(id, user.user_id);
    if (result.success) {
      await loadTransactions();
    } else {
      setError(result.error);
    }
  }

  async function handleBulkUpload(file) {
    const result = await bulkUpload(user.user_id, file);
    if (result.success) {
      await loadTransactions();
    }
    return result;
  }

  return (
    <div className="page">
      <h1 className="page-title">Transactions</h1>
      <p className="page-subtitle">Add, review, and manage your income and expenses.</p>

      <ErrorAlert message={error} onClose={() => setError("")} />

      <div className="transactions-grid">
        <div className="transactions-forms">
          <TransactionForm onSubmit={handleCreate} isSubmitting={isSubmitting} />
          <BulkUpload onUpload={handleBulkUpload} />
        </div>

        <section className="card">
          <div className="card-header">
            <h2>All transactions</h2>
          </div>
          {isLoading ? (
            <Loading label="Loading transactions..." />
          ) : (
            <TransactionTable transactions={transactions} onDelete={handleDelete} />
          )}
        </section>
      </div>
    </div>
  );
}
