import React, { useState } from 'react';
import { SafeAreaView, StyleSheet, Text, View, TextInput, Button, FlatList } from 'react-native';

export default function App() {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [items, setItems] = useState([]);
  const [goal, setGoal] = useState('');

  const addItem = () => {
    if (!description || !amount) return;
    const newItem = { id: Date.now().toString(), description, amount: parseFloat(amount) };
    setItems([...items, newItem]);
    setDescription('');
    setAmount('');
  };

  const calcularSugestao = () => {
    const total = items.reduce((acc, item) => acc + item.amount, 0);
    const media = total / (items.length || 1);
    let sugestao = '';
    if (goal && total > parseFloat(goal)) {
      sugestao = `Você excedeu sua meta. Considere reduzir gastos.`;
    } else {
      const alto = items.find(i => i.amount > media * 2);
      if (alto) {
        sugestao = `Reduza despesas em '${alto.description}'`;
      } else {
        sugestao = `Seus gastos estão sob controle.`;
      }
    }
    return sugestao;
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Controle de Gastos</Text>
      <View style={styles.row}>
        <TextInput
          style={styles.input}
          placeholder="Descrição"
          value={description}
          onChangeText={setDescription}
        />
        <TextInput
          style={styles.input}
          placeholder="Valor"
          keyboardType="numeric"
          value={amount}
          onChangeText={setAmount}
        />
        <Button title="Adicionar" onPress={addItem} />
      </View>
      <TextInput
        style={styles.input}
        placeholder="Meta de gastos"
        keyboardType="numeric"
        value={goal}
        onChangeText={setGoal}
      />
      <FlatList
        data={items}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <Text style={styles.item}>{item.description}: R$ {item.amount.toFixed(2)}</Text>
        )}
      />
      <View style={styles.suggestionBox}>
        <Text style={styles.suggestionTitle}>Sugestão de IA:</Text>
        <Text>{calcularSugestao()}</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 40,
    padding: 16
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    marginRight: 8,
    flex: 1
  },
  item: {
    padding: 4
  },
  suggestionBox: {
    marginTop: 16,
    padding: 8,
    borderWidth: 1,
    borderColor: '#aaa',
    borderRadius: 4
  },
  suggestionTitle: {
    fontWeight: 'bold'
  }
});

