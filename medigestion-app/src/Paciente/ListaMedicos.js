// src/pantallas/ListaMedicos.js
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';

import { datosUsuario } from '../../components/datosUsuario.js';
import { GlobalStyles } from '../../assets/theme/globalStyles.js';

export default function ListaMedicos() {
  const [medicos, setMedicos] = useState([]);
  const [cargando, setCargando] = useState(true);

  const traerMedicos = async () => {
    try {
      const response = await fetch(
        'http://192.168.2.5:5000/api/horarios_medicos',
      );
      const data = await response.json();
      setMedicos(data);
    } catch (error) {
      console.error('Error en el GET:', error);
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    traerMedicos();
  }, []);

  const perfil = datosUsuario(); // Funcion creada para recibir los datos del Usuario

  if (cargando) {
    return (
      <ActivityIndicator size='large' color='#0000ff' style={{ flex: 1 }} />
    );
  }

  return (
    <View style={[GlobalStyles.container]}>
      <Text>{perfil.token}</Text>
      <FlatList
        data={medicos}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.nombre}>{item.nombre}</Text>
            <Text>{item.especialidad}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff' },
  card: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
    marginBottom: 10,
  },
});
