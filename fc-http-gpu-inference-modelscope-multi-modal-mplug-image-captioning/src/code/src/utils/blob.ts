export function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = function () {
      const dataUrl = reader.result as string;
      const base64 = dataUrl?.split(',')[1];
      resolve(base64);
    };
    reader.readAsDataURL(blob);
  });
}

export function getBase64Src(b64: string) {
  return `data:image/png;base64,${b64}`;
}
