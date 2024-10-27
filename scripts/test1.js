function describePerson(person) {
    return [
      'Name: ', 
      person.name, 
      ', Age: ', 
      person.age, 
      ', Hobbies: ', 
      ...person.hobbies
    ].reduce((acc, curr) => acc + curr, ' ');
  }

const person = {
    name: 'Alice',
    age: 30,
    hobbies: ['reading', 'cycling', 'swimming']
  };
  
  console.log(describePerson(person)); 