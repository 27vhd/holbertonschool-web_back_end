export default function taskBlock(trueOrFalse) {
  const task = false;
  let task2 = true;

  if (trueOrFalse) {
    const task = true;
    const task2 = false;
  }

  return [task, task2];
}
