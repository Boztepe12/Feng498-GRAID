import React, { useEffect, useState } from 'react';
import { FlatList, ActivityIndicator, View, Text } from 'react-native';


export default function EspRecivedList() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    
    useEffect(() => {
        const fetchData = async () => {
        try {
            const response = await fetch('http://your-esp-endpoint/data');
            if (!response.ok) {
            throw new Error(`HTTP Hatası: ${response.status}`);
            }
            const data = await response.json();
            setData(data);
        } catch (error) {
            console.error('Veriler çekilemedi:', error);
            setError(true);
        }
        setLoading(false);
        }
        fetchData();
    }, []);

    if (loading) {
        return (
        <View className='container'>
            <ActivityIndicator size="large" color="#0000ff" />
        </View>
        );
    }

    if (error) {
        return (
        <View className='container bg-danger'>
            <Text className='text-red'>Veriler çekilemedi.</Text>
        </View>
        );
    }

    return (
        <FlatList
        data={data}
        // keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
            <View className='container'>
                {/* <Text >{item.value}</Text> */}
                <Text >Degerler</Text>
            </View>
        )}
        />
    );
}