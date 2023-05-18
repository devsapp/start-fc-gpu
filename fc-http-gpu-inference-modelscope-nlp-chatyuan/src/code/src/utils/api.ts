export async function getEndpoint() {
    while (true) {
      const endpoint = (window as any)?.['ENDPOINT'] 
      if (!!endpoint) return endpoint

      await new Promise(r => setTimeout(r, 500));
    }
}