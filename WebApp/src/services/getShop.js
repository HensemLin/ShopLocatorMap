const getShop = async (url, api_key) => {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: { "X-API-KEY": api_key },
    });

    if (!response.ok) {
      throw new Error(`failed to send request to ${url}`);
    }
    const output = await response.json();

    return output;
  } catch (error) {
    console.error(`Error sending request to ${url}: ${error}`);
    return null;
  }
};

export default getShop;
