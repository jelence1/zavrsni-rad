# zavrsni-rad
Repozitorij za Završni rad.

Link na prezentaciju završnog rada: https://prezi.com/p/2qmupueezihz/?present=1


## Bežični prijenos audio signala putem BLE sučelja razvojnog sustava STM32WB5MM-DK
U ovom radu implementiran je sustav za prijam, prikaz i obradu audio signala korištenjem razvojnog sustava STM32WB5MM-DK. Korištene su biblioteke koje omogućavaju snimanje zvuka MEMS mikrofonom na razvojnom sustavu. Korišteno je BLE sučelje za prijenos audio signala s razvojnog sustava na računalo. Razvijeno je grafičko korisničko sučelje za snimanje zvuka i vizualizaciju ranije snimljenih podataka korištenjem razvojnog alata PyQt. Aplikacija se izvodi na operacijskom sustavu Linux. Provedena je analiza zvučnih zapisa hrkanja snimljenih razvijenim sustavom.

## 
### code
Direktorij u kojem se nalazi izvorni kod.

#### audioDumps
Tu se nalaze RAW datoteke koje se mogu pokrenuti u Audacityju: File > Import > Raw Data \
Postavke za pokretanje (ili Detect): 
  - Encoding: Signed 16-bit PCM
  - Byte order: Little-endian
  - Start offset: 0 bytes
  - Amount to import: 100%
  - Sample rate: **16000 Hz**

### documentation 
Direktorij u kojem se nalaze slike i Latex datoteke za završni rad.

Ovdje su također prikazi korisničkog sučelja.


