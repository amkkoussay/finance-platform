/** Basic email shape check: must contain "@" and a "." in the domain part. */
export function validateEmail(email) {
  if (!email || !email.includes("@")) return "Please enter a valid email address.";
  const domain = email.split("@")[1] || "";
  if (!domain.includes(".")) return "Please enter a valid email address.";
  return "";
}

/** Password must be at least 6 characters; optionally must match a confirmation. */
export function validatePassword(password, confirmPassword) {
  if (!password || password.length < 6) {
    return "Password must be at least 6 characters.";
  }
  if (confirmPassword !== undefined && password !== confirmPassword) {
    return "Passwords do not match.";
  }
  return "";
}

/** Amount must be a positive number. */
export function validateAmount(amount) {
  const value = Number(amount);
  if (Number.isNaN(value)) return "Amount must be a number.";
  if (value <= 0) return "Amount must be greater than zero.";
  return "";
}
