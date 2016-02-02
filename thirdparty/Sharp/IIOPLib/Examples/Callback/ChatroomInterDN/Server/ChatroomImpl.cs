/* ChatroomImpl.cs
 *
 * Project: IIOP.NET
 * Examples
 *
 * WHEN      RESPONSIBLE
 * 09.09.03  Dominic Ullmann (DUL), dominic.ullmann -at- elca.ch
 *
 * Copyright 2003 ELCA Informatique SA
 * Av. de la Harpe 22-24, 1000 Lausanne 13, Switzerland
 * www.elca.ch
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */


using System;
using Ch.Elca.Iiop.Idl;

namespace Ch.Elca.Iiop.Demo.Chatroom {


    /// <summary>the chatroom Implementation</sumamry>
    [SupportedInterface(typeof(IChatroom))]
    public class ChatroomImpl : MarshalByRefObject, IChatroom {


        public override object InitializeLifetimeService() {
            // live forever
            return null;
        }


        public void BroadCast(Message msg) {
            ChatroomServer server = ChatroomServer.GetSingleton();
            MessageListener[] listeners = server.GetClients();
            foreach (MessageListener listener in listeners) {
                /// a oneway call, no answer!
                listener.NotifyMessage(msg);
            }
        }
    
        public void RegisterMe(MessageListener listener, String forUser) {
            ChatroomServer server = ChatroomServer.GetSingleton();
            server.AddClient(listener, forUser);
        }    
    
        public void UnregisterMe(String userName) {
            ChatroomServer server = ChatroomServer.GetSingleton();
            server.RemoveClient(userName);
        }
    
    }

}

