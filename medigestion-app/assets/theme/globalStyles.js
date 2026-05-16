import { StyleSheet } from 'react-native';

export const Colors = {
  background: '#f4f6f8',
  text: '#fff',
  error: '#FF5252',
  primary: '#28a745',
  secondary: '#007bff',
};

export const GlobalStyles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    padding: 20,
  },

  buttonMain: {
    alignItems: 'center',
    borderRadius: 10,
    backgroundColor: Colors.primary,
    padding: 18,
  },

  textbutton: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18,
  },

  logo: {
    width: 285,
    height: 130,
    resizeMode: 'container',
  },

  subtitle: {
    fontWeight: 'bold',
    fontSize: 18,
    padding: 10,
    textAlign: 'center',
  },
  input: {
    backgroundColor: '',
    paddingHorizontal: 15,
    paddingVertical: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '',
    marginBottom: 15,
    fontSize: 16,
  },

  tittle: {
    fontWeight: 'bold',
    fontSize: 30,
    padding: 15,
    textAlign: 'center',
  },
});
