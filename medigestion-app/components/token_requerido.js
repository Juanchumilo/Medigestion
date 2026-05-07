import { useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Funcion para hacer la verificación del token

export const verificarToken = () => {
  const [autorizado, setAutorizado] = useState(false);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const verificar = async () => {
      try {
        const token = await AsyncStorage.getItem('token_usuario');

        if (!token) {
          setAutorizado(false);
          return;
        }

        const response = await fetch(
          'http://192.168.2.5:5000/api/verificar_token',
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (response.status == 200) {
          setAutorizado(true);
        } else {
          setAutorizado(false);
        }
      } catch (error) {
        console.error('Error verificando el token', error);
        setAutorizado(false);
      } finally {
        setCargando(false);
      }
    };

    verificar();
  }, []);
  return { autorizado, cargando };
};
