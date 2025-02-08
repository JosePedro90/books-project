export const formatPublicationYear = (
  year: number | string | null | undefined
): string => {
  if (year == null) return "";

  const yearNum = typeof year === "number" ? year : Number(year);

  if (isNaN(yearNum)) return "Invalid Year";

  return yearNum < 0 ? `${Math.abs(yearNum)} BC` : `${yearNum}`;
};
