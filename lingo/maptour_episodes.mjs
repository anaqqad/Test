// Episodes for maptour.mjs. id = ISO 3166 numeric (world-atlas), flag = flag-icons code.
// Counts follow each country's constitution or law; the "unit" says what kind of status it is.
export const EPISODES = {
  official: {
    title: "Countries With the Most Official Languages",
    cold: "ONE COUNTRY HAS<br>37 OFFICIAL LANGUAGES.<br>GUESS WHICH.",
    titleLines: ["COUNTRIES WITH THE MOST", "OFFICIAL LANGUAGES", "WHO HAS THE MOST?"],
    outro: "Which one surprised you? 👇",
    items: [
      { id: "756", flag: "ch", name: "SWITZERLAND", unit: "NATIONAL LANGUAGES", langs: ["German", "French", "Italian", "Romansh"] },
      { id: "702", flag: "sg", name: "SINGAPORE", unit: "OFFICIAL LANGUAGES", maxZoom: 120, langs: ["English", "Malay", "Mandarin", "Tamil"] },
      { id: "710", flag: "za", name: "SOUTH AFRICA", unit: "OFFICIAL LANGUAGES", langs: ["Afrikaans", "English", "isiNdebele", "isiXhosa", "isiZulu", "Sepedi", "Sesotho", "Setswana", "siSwati", "Tshivenda", "Xitsonga", "SA Sign Language"] },
      { id: "716", flag: "zw", name: "ZIMBABWE", unit: "OFFICIAL LANGUAGES", langs: ["Chewa", "Chibarwe", "English", "Kalanga", "Koisan", "Nambya", "Ndau", "Ndebele", "Shangani", "Shona", "Sign language", "Sotho", "Tonga", "Tswana", "Venda", "Xhosa"] },
      { id: "356", flag: "in", name: "INDIA", unit: "SCHEDULED LANGUAGES", langs: ["Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", "Nepali", "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu"] },
      { id: "068", flag: "bo", name: "BOLIVIA", unit: "OFFICIAL LANGUAGES", langs: ["Spanish", "Aymara", "Araona", "Baure", "Bésiro", "Canichana", "Cavineño", "Cayubaba", "Chácobo", "Chimán", "Ese Ejja", "Guaraní", "Guarasu'we", "Guarayu", "Itonama", "Leco", "Machajuyai-Kallawaya", "Machineri", "Maropa", "Mojeño-Trinitario", "Mojeño-Ignaciano", "Moré", "Mosetén", "Movima", "Pacawara", "Puquina", "Quechua", "Sirionó", "Tacana", "Tapieté", "Toromona", "Uru-Chipaya", "Weenhayek", "Yaminawa", "Yuki", "Yuracaré", "Zamuco"] },
    ],
  },
};
