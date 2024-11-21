export const queryIndex = async (text: string) => {
    const response = await fetch(`http://localhost:5601/query?text=${text}`);
    return await response.json();
  };
  