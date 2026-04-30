export const capitalizarNombre = (texto) => {
    if (!texto) return '';
    
    return texto
        .trim() // Limpia espacios basura al inicio y final
        .toLowerCase() 
        .replace(/\b\w/g, (char) => char.toUpperCase());
};