import { demoAccess, demoEvents, demoSellers, demoSyncStates, demoTransactions } from "@/lib/demo-data";

async function main() {
  console.log("Demo seed preview");
  console.log({
    sellers: demoSellers.length,
    events: demoEvents.length,
    accessLinks: demoAccess.length,
    syncStates: demoSyncStates.length,
    transactions: demoTransactions.length
  });
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
