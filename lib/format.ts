const euroNumber = new Intl.NumberFormat("fr-FR", {
  minimumFractionDigits: 0,
  maximumFractionDigits: 2
});

export function formatMoney(value: number, currency = "EUR") {
  return new Intl.NumberFormat("fr-FR", {
    style: "currency",
    currency,
    maximumFractionDigits: 2
  }).format(value);
}

export function formatNumber(value: number) {
  return euroNumber.format(value);
}

export function formatDateTime(value: string | null) {
  if (!value) return "N/A";

  return new Intl.DateTimeFormat("fr-FR", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}

export function formatRelativeStatus(value: string | null) {
  if (!value) return "Jamais synchronise";
  return `Derniere sync ${formatDateTime(value)}`;
}

export function formatApiLabel(value: string) {
  return value
    .replace(/_/g, " ")
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function toStatusClass(value: string) {
  return value.replace(/_/g, "-").toLowerCase();
}
