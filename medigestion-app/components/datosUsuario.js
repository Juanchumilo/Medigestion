import { useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const datosUsuario = () => {
  const [perfil, setPerfil] = useState(null);

  useEffect(() => {
    const cargarDatos = async () => {
      try {
        const datosString = await AsyncStorage.getItem('datos_usuario');
        if (datosString !== null) {
          const datosReales = JSON.parse(datosString);
          setPerfil(datosReales);
        }
      } catch (error) {
        console.error(
          'Error descifrando datos, por favor ingrese nuevamente',
          error,
        );
      }
    };

    cargarDatos();
  }, []);

  // 2. The data MUST be returned to be used outside
  return perfil;
};
