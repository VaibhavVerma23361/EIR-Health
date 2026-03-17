import remediesData from '../data/remedies.json';

export interface Remedy {
  id: number;
  ailment: string;
  remedy: string;
  ingredients: string;
  instructions: string;
  caution: string;
  note: string;
}

export const remedies: Remedy[] = remediesData as Remedy[];

export const getRemedyByAilment = (ailment: string): Remedy | undefined => {
  return remedies.find(remedy => 
    remedy.ailment.toLowerCase().includes(ailment.toLowerCase())
  );
};

export const searchRemedies = (query: string): Remedy[] => {
  const searchTerm = query.toLowerCase();
  return remedies.filter(remedy => 
    remedy.ailment.toLowerCase().includes(searchTerm) ||
    remedy.remedy.toLowerCase().includes(searchTerm) ||
    remedy.ingredients.toLowerCase().includes(searchTerm) ||
    remedy.note.toLowerCase().includes(searchTerm)
  );
};

export const getRemediesByCategory = (category: string): Remedy[] => {
  const categories: { [key: string]: string[] } = {
    'skin': ['Acne Scars', 'Oily Skin', 'Dry Skin', 'Skin Rashes', 'Chapped Hands', 'Dark Lips'],
    'hair': ['Hair Dandruff', 'Brittle Hair'],
    'digestive': ['Gas Trouble', 'Indigestion', 'Constipation', 'Weak Digestion', 'Stomach Ulcer', 'Low Appetite'],
    'respiratory': ['Dry Cough', 'Cough with Phlegm', 'Nasal Congestion', 'Throat Infection', 'Cold Allergy'],
    'pain': ['Migraine', 'Back Pain', 'Joint Stiffness', 'Sore Muscles', 'Leg Cramps', 'Menstrual Fatigue'],
    'circulation': ['Cold Feet', 'Cold Hands and Feet', 'Varicose Veins'],
    'oral': ['Mouth Odor', 'Bad Breath', 'Tooth Stain', 'Tooth Stain'],
    'general': ['Dehydration', 'Stress', 'Insomnia', 'Anemia', 'Hangover', 'Motion Sickness']
  };

  const categoryAilments = categories[category.toLowerCase()] || [];
  return remedies.filter(remedy => categoryAilments.includes(remedy.ailment));
};

export const getRandomRemedy = (): Remedy => {
  const randomIndex = Math.floor(Math.random() * remedies.length);
  return remedies[randomIndex];
};

export const getRemediesCount = (): number => remedies.length;
