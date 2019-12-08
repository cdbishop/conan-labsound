#include <iostream>
#include <LabSound/extended/LabSound.h>

int main()
{
    auto context = lab::Sound::MakeRealtimeAudioContext(lab::Channels::Stereo);
    if (!context) {
        return 1;
    }
    return 0;
}