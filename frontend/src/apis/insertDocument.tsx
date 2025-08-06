export const insertDocument = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
  
    const response = await fetch("http://localhost:5001/uploadFile", {
      method: "POST",
      body: formData,
    });
    return await response.json();
  };
  