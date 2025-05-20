import React, { useState } from 'react';
import { View, Text, Button, Image, ActivityIndicator, StyleSheet } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Speech from 'expo-speech';
import axios from 'axios';

const HomeScreen = () => {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [image, setImage] = useState(null);

const pickImage = async () => {
  const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
  if (!permissionResult.granted) {
    alert('사진 접근 권한이 필요합니다!');
    return;
  }

  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: false,
    base64: false,
  });

  if (!result.canceled && result.assets.length > 0) {
    const selectedImage = result.assets[0];
    setImage(selectedImage.uri);
  }
};

 const handleDetect = async () => {
  if (!image) return;

  setLoading(true);

  const formData = new FormData();
  formData.append('image', {
    uri: image,
    name: 'photo.jpg',
    type: 'image/jpeg',
  });

  try {
    const response = await axios.post('http://192.168.219.104:5001/detect', formData, {
      headers: {
       // 'Content-Type': 'multipart/form-data',
      },
    });
    const detected = response.data.result;
    setResult(detected);
    Speech.speak(`감지된 객체는 ${detected}입니다.`);
  } catch (error) {
    console.error('객체 인식 오류:', error.message);
    setResult('오류 발생');
    Speech.speak('객체 인식 중 오류가 발생했습니다.');
  } finally {
    setLoading(false);
  }
};


  return (
    <View style={styles.container}>
      <Text style={styles.title}>YOLOv5 객체 인식</Text>
      <Button title="이미지 선택" onPress={pickImage} />
      {image && <Image source={{ uri: image }} style={{ width: 200, height: 200, marginTop: 10 }} />}
      <Button title="객체 인식 시작" onPress={handleDetect} disabled={!image} />
      {loading && <ActivityIndicator size="large" />}
      <Text style={styles.resultText}>{result}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 24, marginBottom: 20 },
  resultText: { fontSize: 18, marginTop: 20 },
});

export default HomeScreen;
