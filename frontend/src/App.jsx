import { useState, useEffect } from 'react';
import { Container, Title, MultiSelect, SimpleGrid, Card, Text, Badge, Center, Loader } from '@mantine/core';
import axios from 'axios';

export default function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [options, setOptions] = useState([]);
  const [selected, setSelected] = useState([]);
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(false);

  // SEARCH EFFECT
  useEffect(() => {
    if (searchQuery.length < 2) {
      setOptions([]);
      return;
    }

    const timer = setTimeout(() => {
      axios.get(`http://localhost:8000/search?q=${searchQuery}`)
        .then(res => {
          // use display_name so Mantine doesn't see duplicates
          const names = res.data.map(m => m.display_name);
          setOptions([...new Set(names)]); // extra safety to ensure uniqueness
        })
        .catch(err => console.error(err));
    }, 400); // wait 400ms after you stop typing

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // RECOMMEND EFFECT
  useEffect(() => {
    if (selected.length > 0) {
      setLoading(true);
      axios.post('http://localhost:8000/recommend', selected)
        .then(res => {
          setRecs(res.data);
          setLoading(false);
        })
        .catch(() => setLoading(false));
    } else {
      setRecs([]);
    }
  }, [selected]);

  return (
    <Container size="md" py="xl">
      <Title order={1} mb="xl" ta="center">🎬 MovieMind</Title>
      
      <MultiSelect
        label="Select movies you liked"
        placeholder="Type to search (e.g. Interstellar, Toy Story)..."
        data={options}
        searchable
        searchValue={searchQuery}
        onSearchChange={setSearchQuery}
        value={selected}
        onChange={setSelected}
        mb={40}
      />

      {loading ? (
        <Center><Loader color="blue" /></Center>
      ) : (
        <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }}>
          {recs.map((movie, i) => (
            <Card key={`${movie.title}-${i}`} shadow="sm" padding="lg" radius="md" withBorder>
              <Text fw={700}>{movie.title}</Text>
              <Badge color="blue" variant="light" mb="sm">
                {movie.release_year}
              </Badge>
              <Text size="sm" c="dimmed" lineClamp={3}>
                {movie.concat}
              </Text>
            </Card>
          ))}
        </SimpleGrid>
      )}
    </Container>
  );
}