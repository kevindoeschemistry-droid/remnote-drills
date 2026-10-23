/** Thrown by a generator when a random draw gives an ugly problem; the registry redraws. */
export class Reject extends Error {}
export const require_ = (c: boolean) => {
  if (!c) throw new Reject();
};
